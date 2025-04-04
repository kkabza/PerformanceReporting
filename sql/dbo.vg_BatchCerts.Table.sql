USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_BatchCerts]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_BatchCerts](
	[CertsID] [int] IDENTITY(1,1) NOT NULL,
	[BatchID] [int] NULL,
	[SequenceID] [int] NULL,
	[PropertyNo] [varchar](50) NULL,
	[UnpaidBalance] [decimal](10, 2) NULL,
	[YourBid] [decimal](10, 2) NULL,
 CONSTRAINT [PK_BatchCerts] PRIMARY KEY CLUSTERED 
(
	[CertsID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
