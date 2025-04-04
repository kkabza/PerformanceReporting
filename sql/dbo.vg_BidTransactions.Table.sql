USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_BidTransactions]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_BidTransactions](
	[BidId] [int] IDENTITY(1,1) NOT NULL,
	[UserId] [uniqueidentifier] NOT NULL,
	[PropertyNo] [varchar](50) NOT NULL,
	[TaxYear] [int] NOT NULL,
	[BidPercent] [decimal](10, 2) NULL,
	[BidTime] [datetime] NOT NULL,
	[BidSource] [varchar](15) NOT NULL,
	[BidStatus] [int] NOT NULL,
	[VGProductID] [int] NULL,
	[SequenceNo] [int] NULL,
	[UnpaidBalance] [money] NULL
) ON [PRIMARY]
GO
