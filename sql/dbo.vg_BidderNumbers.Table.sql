USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_BidderNumbers]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_BidderNumbers](
	[BidderId] [int] IDENTITY(1,1) NOT NULL,
	[VGProductID] [int] NOT NULL,
	[UserId] [uniqueidentifier] NOT NULL,
	[BidderNumber] [varchar](50) NULL,
	[BidBefore] [bit] NULL,
 CONSTRAINT [PK_vg_BidderNumbers] PRIMARY KEY CLUSTERED 
(
	[BidderId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
